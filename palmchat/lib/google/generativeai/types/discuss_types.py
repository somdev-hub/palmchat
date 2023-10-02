# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Type definitions for the discuss service."""

import abc
import dataclasses
from typing import Any, Dict, TypedDict, Union, Iterable, Optional, Tuple, List

import google.ai.generativelanguage_v1beta3 as glm
from google.generativeai.types import safety_types
from google.generativeai.types import citation_types

__all__ = [
    "MessageDict",
    "MessageOptions",
    "MessagesOptions",
    "ExampleDict",
    "ExampleOptions",
    "ExamplesOptions",
    "MessagePromptDict",
    "MessagePromptOptions",
    "ResponseDict",
    "ChatResponse",
    "AuthorError",
]


class MessageDict(TypedDict):
    """A dict representation of a `glm.Message`."""

    author: str
    content: str
    citation_metadata: Optional[citation_types.CitationMetadataDict]


MessageOptions = Union[str, MessageDict, glm.Message]
MESSAGE_OPTIONS = (str, dict, glm.Message)

MessagesOptions = Union[
    MessageOptions,
    Iterable[MessageOptions],
]
MESSAGES_OPTIONS = (MESSAGE_OPTIONS, Iterable)


class ExampleDict(TypedDict):
    """A dict representation of a `glm.Example`."""

    input: MessageOptions
    output: MessageOptions


ExampleOptions = Union[
    Tuple[MessageOptions, MessageOptions],
    Iterable[MessageOptions],
    ExampleDict,
    glm.Example,
]
EXAMPLE_OPTIONS = (glm.Example, dict, Iterable)
ExamplesOptions = Union[ExampleOptions, Iterable[ExampleOptions]]


class MessagePromptDict(TypedDict, total=False):
    """A dict representation of a `glm.MessagePrompt`."""

    context: str
    examples: ExamplesOptions
    messages: MessagesOptions


MessagePromptOptions = Union[
    str,
    glm.Message,
    Iterable[Union[str, glm.Message]],
    MessagePromptDict,
    glm.MessagePrompt,
]
MESSAGE_PROMPT_KEYS = {"context", "examples", "messages"}


class ResponseDict(TypedDict):
    """A dict representation of a `glm.GenerateMessageResponse`."""

    messages: List[MessageDict]
    candidates: List[MessageDict]


@dataclasses.dataclass(init=False)
class ChatResponse(abc.ABC):
    """A chat response from the model.

    * Use `response.last` (settable) for easy access to the text of the last response.
        (`messages[-1]['content']`)
    * Use `response.messages` to access the message history (including `.last`).
    * Use `response.candidates` to access all the responses generated by the model.

    Other attributes are just saved from the arguments to `genai.chat`, so you
    can easily continue a conversation:

    ```
    import google.generativeai as genai

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    response = genai.chat(messages=["Hello."])
    print(response.last) #  'Hello! What can I help you with?'
    response.reply("Can you tell me a joke?")
    ```

    See `genai.chat` for more details.

    Attributes:
        candidates: A list of candidate responses from the model.

            The top candidate is appended to the `messages` field.

            This list will contain a *maximum* of `candidate_count` candidates.
            It may contain fewer (duplicates are dropped), it will contain at least one.

            Note: The `temperature` field affects the variability of the responses. Low
            temperatures will return few candidates. Setting `temperature=0` is deterministic,
            so it will only ever return one candidate.
        filters: This indicates which `types.SafetyCategory`(s) blocked a
           candidate from this response, the lowest `types.HarmProbability`
           that triggered a block, and the `types.HarmThreshold` setting for that category.
           This indicates the smallest change to the `types.SafetySettings` that would be
           necessary to unblock at least 1 response.

           The blocking is configured by the `types.SafetySettings` in the request (or the
           default `types.SafetySettings` of the API).
        messages: Contains all the `messages` that were passed when the model was called,
            plus the top `candidate` message.
        model: The model name.
        context: Text that should be provided to the model first, to ground the response.
        examples: Examples of what the model should generate.
        messages: A snapshot of the conversation history sorted chronologically.
        temperature: Controls the randomness of the output. Must be positive.
        candidate_count: The **maximum** number of generated response messages to return.
        top_k: The maximum number of tokens to consider when sampling.
        top_p: The maximum cumulative probability of tokens to consider when sampling.

    """

    model: str
    context: str
    examples: List[ExampleDict]
    messages: List[Optional[MessageDict]]
    temperature: Optional[float]
    candidate_count: Optional[int]
    candidates: List[MessageDict]
    filters: List[safety_types.ContentFilterDict]
    top_p: Optional[float] = None
    top_k: Optional[float] = None

    @property
    @abc.abstractmethod
    def last(self) -> Optional[str]:
        """A settable property that provides simple access to the last response string

        A shortcut for `response.messages[0]['content']`.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "model": self.model,
            "context": self.context,
            "examples": self.examples,
            "messages": self.messages,
            "temperature": self.temperature,
            "candidate_count": self.candidate_count,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "candidates": self.candidates,
        }
        return result

    @abc.abstractmethod
    def reply(self, message: MessageOptions) -> "ChatResponse":
        "Add a message to the conversation, and get the model's response."
        pass


class AuthorError(Exception):
    """Raised by the `chat` (or `reply`) functions when the author list can't be normalized."""

    pass
