from typing import List, Tuple, Dict

import openai
from byzerllm.utils.openai_utils import completion_with_retry


class CustomSaasAPI:
    def __init__(self, infer_params: Dict[str, str]) -> None:
        self.api_type = infer_params["saas.api_type"]
        self.api_key = infer_params["saas.api_key"]
        self.api_base = infer_params["saas.api_base"]
        self.api_version = infer_params["saas.api_version"]
        self.deployment_id = infer_params["saas.deployment_id"]
        openai.api_type = infer_params["saas.api_type"]
        openai.api_key = infer_params["saas.api_key"]
        openai.api_base = infer_params["saas.api_base"]
        openai.api_version = infer_params["saas.api_version"]

        self.max_retries = 10

     # saas/proprietary
    def get_meta(self):
        return [{
            "model_deploy_type": "saas",
            "backend":"saas"
        }]    

    def stream_chat(self, tokenizer, ins: str, his: List[Tuple[str, str]] = [],
                    max_length: int = 4096,
                    top_p: float = 0.7,
                    temperature: float = 0.9, **kwargs):

        deployment_id = self.deployment_id
        max_retries = self.max_retries

        if "model" in kwargs:
            deployment_id = kwargs["model"]
        if "max_retries" in kwargs:
            max_retries = kwargs["max_retries"]

        messages = his + [{"role": "user", "content": ins}]

        response = None

        try:
            chat_completion = completion_with_retry(
                is_chat_model=True,
                max_retries=max_retries,
                messages=messages,
                deployment_id=deployment_id,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_length
            )
            response = chat_completion.choices[0]["message"]["content"].replace(' .', '.').strip()
        except Exception as e:
            print(f"request azure openai failed: {e}")
            response = f"Exception occurred during the request, please try again: {e}" \
                if response is None or response == "" else response

        return [(response, "")]
