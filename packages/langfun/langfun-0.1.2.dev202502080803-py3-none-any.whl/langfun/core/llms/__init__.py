# Copyright 2023 The Langfun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""langfun LLM implementations."""

# pylint: disable=g-importing-member
# pylint: disable=g-bad-import-order
# pylint: disable=g-import-not-at-top

# LMs for testing.
from langfun.core.llms.fake import Fake
from langfun.core.llms.fake import Echo
from langfun.core.llms.fake import StaticMapping
from langfun.core.llms.fake import StaticResponse
from langfun.core.llms.fake import StaticSequence

# Compositional models.
from langfun.core.llms.compositional import RandomChoice

# Base models by request/response protocol.
from langfun.core.llms.rest import REST
from langfun.core.llms.openai_compatible import OpenAICompatible
from langfun.core.llms.gemini import Gemini
from langfun.core.llms.anthropic import Anthropic

# Base models by serving platforms.
from langfun.core.llms.vertexai import VertexAI
from langfun.core.llms.groq import Groq

# Gemini models.
from langfun.core.llms.google_genai import GenAI
from langfun.core.llms.google_genai import Gemini2Flash
from langfun.core.llms.google_genai import Gemini2ProExp_20250205
from langfun.core.llms.google_genai import Gemini2FlashThinkingExp_20250121
from langfun.core.llms.google_genai import GeminiFlash2_0ThinkingExp_20241219
from langfun.core.llms.google_genai import GeminiFlash2_0Exp
from langfun.core.llms.google_genai import GeminiExp_20241206
from langfun.core.llms.google_genai import GeminiExp_20241114
from langfun.core.llms.google_genai import GeminiPro1_5
from langfun.core.llms.google_genai import GeminiPro1_5_002
from langfun.core.llms.google_genai import GeminiPro1_5_001
from langfun.core.llms.google_genai import GeminiFlash1_5
from langfun.core.llms.google_genai import GeminiFlash1_5_002
from langfun.core.llms.google_genai import GeminiFlash1_5_001
from langfun.core.llms.google_genai import GeminiPro1

from langfun.core.llms.vertexai import VertexAIGemini
from langfun.core.llms.vertexai import VertexAIGemini2Flash
from langfun.core.llms.vertexai import VertexAIGemini2ProExp_20250205
from langfun.core.llms.vertexai import VertexAIGemini2FlashThinkingExp_20250121
from langfun.core.llms.vertexai import VertexAIGeminiFlash2_0ThinkingExp_20241219
from langfun.core.llms.vertexai import VertexAIGeminiFlash2_0Exp
from langfun.core.llms.vertexai import VertexAIGeminiExp_20241206
from langfun.core.llms.vertexai import VertexAIGeminiExp_20241114
from langfun.core.llms.vertexai import VertexAIGeminiPro1_5
from langfun.core.llms.vertexai import VertexAIGeminiPro1_5_002
from langfun.core.llms.vertexai import VertexAIGeminiPro1_5_001
from langfun.core.llms.vertexai import VertexAIGeminiFlash1_5
from langfun.core.llms.vertexai import VertexAIGeminiFlash1_5_002
from langfun.core.llms.vertexai import VertexAIGeminiFlash1_5_001
from langfun.core.llms.vertexai import VertexAIGeminiPro1

# OpenAI models.
from langfun.core.llms.openai import OpenAI

from langfun.core.llms.openai import GptO3Mini
from langfun.core.llms.openai import GptO1
from langfun.core.llms.openai import GptO1Preview
from langfun.core.llms.openai import GptO1Preview_20240912
from langfun.core.llms.openai import GptO1Mini
from langfun.core.llms.openai import GptO1Mini_20240912

from langfun.core.llms.openai import Gpt4oMini
from langfun.core.llms.openai import Gpt4oMini_20240718
from langfun.core.llms.openai import Gpt4o
from langfun.core.llms.openai import Gpt4o_20241120
from langfun.core.llms.openai import Gpt4o_20240806
from langfun.core.llms.openai import Gpt4o_20240513

from langfun.core.llms.openai import Gpt4Turbo
from langfun.core.llms.openai import Gpt4Turbo_20240409
from langfun.core.llms.openai import Gpt4TurboPreview
from langfun.core.llms.openai import Gpt4TurboPreview_20240125
from langfun.core.llms.openai import Gpt4TurboPreview_20231106
from langfun.core.llms.openai import Gpt4VisionPreview
from langfun.core.llms.openai import Gpt4VisionPreview_20231106
from langfun.core.llms.openai import Gpt4
from langfun.core.llms.openai import Gpt4_20230613

from langfun.core.llms.openai import Gpt4_32K
from langfun.core.llms.openai import Gpt4_32K_20230613

from langfun.core.llms.openai import Gpt35Turbo
from langfun.core.llms.openai import Gpt35Turbo_20240125
from langfun.core.llms.openai import Gpt35Turbo_20231106
from langfun.core.llms.openai import Gpt35Turbo_20230613
from langfun.core.llms.openai import Gpt35Turbo16K
from langfun.core.llms.openai import Gpt35Turbo16K_20230613

# For backward compatibility.
Gpt4TurboPreview_0125 = Gpt4TurboPreview_20240125
Gpt4TurboPreview_1106 = Gpt4TurboPreview_20231106
Gpt4VisionPreview_1106 = Gpt4VisionPreview_20231106
Gpt4_0613 = Gpt4_20230613
Gpt4_32K_0613 = Gpt4_32K_20230613
Gpt35Turbo_0125 = Gpt35Turbo_20240125
Gpt35Turbo_1106 = Gpt35Turbo_20231106
Gpt35Turbo_0613 = Gpt35Turbo_20230613
Gpt35Turbo16K_0613 = Gpt35Turbo16K_20230613

from langfun.core.llms.openai import Gpt35

from langfun.core.llms.openai import Gpt3
from langfun.core.llms.openai import Gpt3Curie
from langfun.core.llms.openai import Gpt3Babbage
from langfun.core.llms.openai import Gpt3Ada

# Anthropic models.

from langfun.core.llms.anthropic import Claude35Sonnet
from langfun.core.llms.anthropic import Claude35Sonnet20241022
from langfun.core.llms.anthropic import Claude35Sonnet20240620
from langfun.core.llms.anthropic import Claude3Opus
from langfun.core.llms.anthropic import Claude3Sonnet
from langfun.core.llms.anthropic import Claude3Haiku

from langfun.core.llms.vertexai import VertexAIAnthropic
from langfun.core.llms.vertexai import VertexAIClaude3_5_Sonnet_20241022
from langfun.core.llms.vertexai import VertexAIClaude3_5_Sonnet_20240620
from langfun.core.llms.vertexai import VertexAIClaude3_5_Haiku_20241022
from langfun.core.llms.vertexai import VertexAIClaude3_Opus_20240229

# Misc open source models.

# Gemma models.
from langfun.core.llms.groq import GroqGemma2_9B_IT
from langfun.core.llms.groq import GroqGemma_7B_IT

# Llama models.
from langfun.core.llms.vertexai import VertexAILlama
from langfun.core.llms.vertexai import VertexAILlama3_2_90B
from langfun.core.llms.vertexai import VertexAILlama3_1_405B
from langfun.core.llms.vertexai import VertexAILlama3_1_70B
from langfun.core.llms.vertexai import VertexAILlama3_1_8B

from langfun.core.llms.groq import GroqLlama3_2_3B
from langfun.core.llms.groq import GroqLlama3_2_1B
from langfun.core.llms.groq import GroqLlama3_1_70B
from langfun.core.llms.groq import GroqLlama3_1_8B
from langfun.core.llms.groq import GroqLlama3_70B
from langfun.core.llms.groq import GroqLlama3_8B
from langfun.core.llms.groq import GroqLlama2_70B

# Mistral models.
from langfun.core.llms.vertexai import VertexAIMistral
from langfun.core.llms.vertexai import VertexAIMistralLarge_20241121
from langfun.core.llms.vertexai import VertexAIMistralLarge_20240724
from langfun.core.llms.vertexai import VertexAIMistralNemo_20240724
from langfun.core.llms.vertexai import VertexAICodestral_20250113
from langfun.core.llms.vertexai import VertexAICodestral_20240529

from langfun.core.llms.groq import GroqMistral_8x7B

# DeepSeek models.
from langfun.core.llms.deepseek import DeepSeek
from langfun.core.llms.deepseek import DeepSeekChat
from langfun.core.llms.deepseek import DeepSeekReasoner

# Whisper models.
from langfun.core.llms.groq import GroqWhisper_Large_v3
from langfun.core.llms.groq import GroqWhisper_Large_v3Turbo

# LLaMA C++ models.
from langfun.core.llms.llama_cpp import LlamaCppRemote


# Placeholder for Google-internal imports.

# Include cache as sub-module.
from langfun.core.llms import cache

# pylint: enable=g-import-not-at-top
# pylint: enable=g-bad-import-order
# pylint: enable=g-importing-member
