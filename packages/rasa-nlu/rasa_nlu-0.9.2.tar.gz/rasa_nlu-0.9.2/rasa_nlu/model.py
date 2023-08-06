from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import io
import json
import logging
import os

import copy
from builtins import object
from builtins import str
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

import rasa_nlu
from rasa_nlu import components
from rasa_nlu.components import Component
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.persistor import Persistor
from rasa_nlu.training_data import TrainingData, Message
from rasa_nlu.utils import create_dir

logger = logging.getLogger(__name__)


class InvalidModelError(Exception):
    """Raised when a model failed to load.

    Attributes:
        message -- explanation of why the model is invalid
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Metadata(object):
    """Captures all necessary information about a model to load it and prepare it for usage."""

    @staticmethod
    def load(model_dir):
        # type: (Text) -> 'Metadata'
        """Loads the metadata from a models directory."""
        try:
            with io.open(os.path.join(model_dir, 'metadata.json'), encoding="utf-8") as f:
                data = json.loads(f.read())
            return Metadata(data, model_dir)
        except Exception as e:
            raise InvalidModelError("Failed to load model metadata. {}".format(e))

    def __init__(self, metadata, model_dir):
        # type: (Dict[Text, Any], Optional[Text]) -> None

        self.metadata = metadata
        self.model_dir = model_dir

    def get(self, property_name, default=None):
        return self.metadata.get(property_name, default)

    @property
    def language(self):
        # type: () -> Optional[Text]
        """Language of the underlying model"""

        return self.get('language')

    @property
    def pipeline(self):
        # type: () -> List[Text]
        """Names of the processing pipeline elements."""

        return self.get('pipeline', [])

    def persist(self, model_dir):
        # type: (Text) -> None
        """Persists the metadata of a model to a given directory."""

        metadata = self.metadata.copy()

        metadata.update({
            "trained_at": datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
            "rasa_nlu_version": rasa_nlu.__version__,
        })

        with io.open(os.path.join(model_dir, 'metadata.json'), 'w') as f:
            f.write(str(json.dumps(metadata, indent=4)))


class Trainer(object):
    """Given a pipeline specification and configuration this trainer will load the data and train all components."""

    # Officially supported languages (others might be used, but might fail)
    SUPPORTED_LANGUAGES = ["de", "en"]

    def __init__(self, config, component_builder=None, skip_validation=False):
        # type: (RasaNLUConfig, Optional[ComponentBuilder], bool) -> None

        self.config = config
        self.skip_validation = skip_validation
        self.training_data = None       # type: Optional[TrainingData]
        self.pipeline = []              # type: List[Component]
        if component_builder is None:
            # If no builder is passed, every interpreter creation will result in a new builder.
            # hence, no components are reused.
            component_builder = components.ComponentBuilder()

        # Before instantiating the component classes, lets check if all required packages are available
        if not self.skip_validation:
            components.validate_requirements(config.pipeline)

        # Transform the passed names of the pipeline components into classes
        for component_name in config.pipeline:
            component = component_builder.create_component(component_name, config)
            self.pipeline.append(component)

    def train(self, data):
        # type: (TrainingData) -> Interpreter
        """Trains the underlying pipeline by using the provided training data."""

        self.training_data = copy.deepcopy(data)

        context = {}        # type: Dict[Text, Any]

        for component in self.pipeline:
            updates = component.provide_context()
            if updates:
                context.update(updates)

        # Before training the component classes, lets check if all arguments are provided
        if not self.skip_validation:
            components.validate_arguments(self.pipeline, context)

        for component in self.pipeline:
            logger.info("Starting to train component {}".format(component.name))
            updates = component.train(data, self.config, **context)
            logger.info("Finished training component.")
            if updates:
                context.update(updates)

        return Interpreter(self.pipeline, context)

    def persist(self, path, persistor=None, model_name=None):
        # type: (Text, Optional[Persistor], Text) -> Text
        """Persist all components of the pipeline to the passed path. Returns the directory of the persited model."""

        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        metadata = {
            "language": self.config["language"],
            "pipeline": [component.name for component in self.pipeline],
        }

        if model_name is None:
            dir_name = os.path.join(path, "model_" + timestamp)
        else:
            dir_name = os.path.join(path, model_name)

        create_dir(dir_name)

        if self.training_data:
            metadata.update(self.training_data.persist(dir_name))

        for component in self.pipeline:
            update = component.persist(dir_name)
            if update:
                metadata.update(update)

        Metadata(metadata, dir_name).persist(dir_name)

        if persistor is not None:
            persistor.save_tar(dir_name)
        logger.info("Successfully saved model into '{}'".format(os.path.abspath(dir_name)))
        return dir_name


class Interpreter(object):
    """Use a trained pipeline of components to parse text messages"""

    # Defines all attributes (and their default values) that will be returned by `parse`
    @staticmethod
    def default_output_attributes():
        return {"intent": {"name": "", "confidence": 0.0}, "entities": []}

    @staticmethod
    def load(model_metadata, config, component_builder=None, skip_valdation=False):
        # type: (Metadata, RasaNLUConfig, Optional[ComponentBuilder], bool) -> Interpreter
        """Load a stored model and its components defined by the provided metadata."""
        context = {}

        if component_builder is None:
            # If no builder is passed, every interpreter creation will result in a new builder.
            # hence, no components are reused.
            component_builder = components.ComponentBuilder()

        pipeline = []

        # Before instantiating the component classes, lets check if all required packages are available
        if not skip_valdation:
            components.validate_requirements(model_metadata.pipeline)

        for component_name in model_metadata.pipeline:
            component = component_builder.load_component(
                    component_name, model_metadata.model_dir, model_metadata, **context)
            try:
                updates = component.provide_context()
                if updates:
                    context.update(updates)
                pipeline.append(component)
            except components.MissingArgumentError as e:
                raise Exception("Failed to initialize component '{}'. {}".format(component.name, e))

        return Interpreter(pipeline, context, model_metadata)

    def __init__(self, pipeline, context, model_metadata=None):
        # type: (List[Component], Dict[Text, Any], Optional[Metadata]) -> None

        self.pipeline = pipeline
        self.context = context if context is not None else {}
        self.model_metadata = model_metadata

    def parse(self, text, time=None):
        # type: (Text) -> Dict[Text, Any]
        """Parse the input text, classify it and return an object containing its intent and entities."""

        if not text:
            # Not all components are able to handle empty strings. So we need to prevent that...
            # This default return will not contain all output attributes of all components,
            # but in the end, no one should pass an empty string in the first place.
            output = self.default_output_attributes()
            output["text"] = ""
            return output

        message = Message(text, self.default_output_attributes(), time=time)

        for component in self.pipeline:
            component.process(message, **self.context)

        output = self.default_output_attributes()
        output.update(message.as_dict(only_output_properties=True))
        return output
