from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .core import Agent
import asyncio
from tqdm import tqdm

class TestCase(BaseModel):
    input: str
    expected: str
    
class EvalResult(BaseModel):
    input: str
    output: str
    expected: str
    score: int  # 0 to 1
    reasoning: str

class Evaluator:
    """
    LLM-as-a-Judge Evaluator.
    Runs a dataset against an agent and scores the results using a Judge agent.
    """
    def __init__(self, agent: Agent, judge_model: str = "gpt-4o"):
        self.agent = agent
        self.judge = Agent(
            name="Judge", 
            model=judge_model,
            system="You are an impartial judge evaluating the quality of AI responses. "
                   "Compare the ACTUAL output with the EXPECTED output. "
                   "Return JSON with 'score' (0 or 1) and 'reasoning'."
        )

    class JudgeDecision(BaseModel):
        score: int
        reasoning: str

    async def _evaluate_single(self, case: TestCase) -> EvalResult:
        # Get actual response
        # Note: We use the sync ask() here, but run in thread if needed. 
        # For simplicity in this v0.8 MVP, we assume fast execution.
        if hasattr(self.agent, 'ask_async'):
             actual = await self.agent.ask(case.input)
        else:
             actual = self.agent.ask(case.input)

        # Judge the response
        prompt = f"""
        INPUT: {case.input}
        EXPECTED: {case.expected}
        ACTUAL: {actual}
        
        Is the ACTUAL response correct based on the EXPECTED response?
        If it conveys the same meaning, it is correct.
        """
        
        decision = self.judge.ask(prompt, response_model=self.JudgeDecision)
        
        return EvalResult(
            input=case.input,
            output=str(actual),
            expected=case.expected,
            score=decision.score,
            reasoning=decision.reasoning
        )

    async def run(self, dataset: List[Dict[str, str]]) -> List[EvalResult]:
        """Run evaluation on a dataset."""
        results = []
        cases = [TestCase(**d) for d in dataset]
        
        print(f"📉 Starting Evaluation on {len(cases)} cases...")
        
        for case in tqdm(cases):
            result = await self._evaluate_single(case)
            results.append(result)
            
        # Calculate summary
        total_score = sum(r.score for r in results)
        accuracy = (total_score / len(results)) * 100
        
        print(f"\n✅ Evaluation Complete")
        print(f"Accuracy: {accuracy:.1f}%")
        
        return results
