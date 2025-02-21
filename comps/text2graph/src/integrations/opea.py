# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time
from typing import Annotated, Optional
from langchain.agents.agent_types import AgentType
from langchain_huggingface import HuggingFaceEndpoint
from pydantic import BaseModel, Field
from comps import CustomLogger, OpeaComponent, OpeaComponentRegistry, ServiceType
from comps.text2graph.src.integrations.graph_agent import TripletManager, TripletBuilder, TripletExtractor
##from comps.text2graph.src.integrations.triplet_manager import TripletManager
##from comps.text2graph.src.integrations.triplet_builder import TripletBuilder
##from comps.text2graph.src.integrations.triplet_extractor import TripletExtractor

logger = CustomLogger("comps-text2graph")
logflag = os.getenv("LOGFLAG", False)

graph_params = {
    "max_string_length": 3600,
}

generation_params = {
    "max_new_tokens": 1024,
    "top_k": 10,
    "top_p": 0.95,
    "temperature": 0.01,
    "repetition_penalty": 1.03,
    "streaming": True,
}

#TGI_LLM_ENDPOINT = os.environ.get("TGI_LLM_ENDPOINT")
#
#llm = HuggingFaceEndpoint(
#    endpoint_url=TGI_LLM_ENDPOINT,
#    task="text-generation",
#    **generation_params,
#    )

class Input(BaseModel):
    input_text: str
    #conn_str: Optional[PostgresConnection] = None

@OpeaComponentRegistry.register("OPEA_TEXT2GRAPH")
class OpeaText2GRAPH(OpeaComponent):
    """
       A specialized text to graph triplet converter
    """

    def __init__(self, name: str, description: str, config: dict = None):
        super().__init__(name, ServiceType.TEXT2GRAPH.name.lower(), description, config)
        health_status = self.check_health()
        if not health_status:
            logger.error("OpeaText2GRAPH health check failed.")

    async def check_health(self) -> bool:
        """Checks the health of the TGI service.
        Returns:
            bool: True if the service is reachable and healthy, False otherwise.
        """
        try:
            #response = llm.generate(["Hello, how are you?"])
            return True
        except Exception as e:
            return False

    async def invoke(self, input_text: str):
       """Invokes the text2graph service to generate graph(s) for the provided input.
        input:
            input: text document
        Returns:
            text : dict
       """

       tb = TripletBuilder()
       graph_triplets = await tb.extract_graph(input_text)

       #tm = TripletManager()
       #entity, relation = tm.write_to_csv(WRITE_TO_CSV=False)

       result = {"graph_triplets": graph_triplets}

       return result
