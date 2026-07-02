"""
LangGraph Pipeline Tests
Author: Muhammad Atif

Tests the full agentic RAG graph pipeline including:
- Simple path routing
- Complex path routing  
- Retrieval
- Verification
- Answer generation

Usage:
    python -m tests.test_graph
"""

from graph.workflow import graph
import time

# ================================================================
# TEST RUNNER
# ================================================================

passed = 0
failed = 0


def run_test(test_name: str, question: str, expected_path: str, should_find_answer: bool):

    global passed, failed

    print(f"\nTEST: {test_name}")
    print(f"QUESTION: {question}")
    print(f"EXPECTED PATH: {expected_path}")

    try:
        time.sleep(4)  # 4 second gap between each Gemini call
        output = graph.invoke({"question": question})

        query_type  = output.get("query_type", "unknown")
        is_verified = output.get("is_verified", False)
        answer      = output.get("answer", "").strip()

        print(f"ACTUAL PATH  : {query_type}")
        print(f"VERIFIED     : {is_verified}")
        print(f"ANSWER       : {answer[:200]}")

        # Check routing
        routing_correct = query_type == expected_path

        # Check answer quality
        answer_empty   = len(answer) == 0
        answer_refused = "not found in documents" in answer.lower() or "i don't have" in answer.lower()

        if should_find_answer:
            answer_ok = not answer_empty and not answer_refused
        else:
            answer_ok = answer_refused or answer_empty

        if routing_correct and answer_ok:
            print("RESULT: PASSED")
            passed += 1
        else:
            if not routing_correct:
                print(f"RESULT: FAILED - wrong path, expected {expected_path} got {query_type}")
            if not answer_ok:
                print(f"RESULT: FAILED - answer quality check failed")
            failed += 1

    except Exception as e:
        print(f"RESULT: ERROR - {e}")
        failed += 1


# ================================================================
# SIMPLE PATH TESTS
# These questions should route to simple path and find answers
# ================================================================

run_test(
    test_name        = "Simple - Direct fact from Panaversity",
    question         = "What is Panaversity?",
    expected_path    = "simple",
    should_find_answer = True
)

run_test(
    test_name        = "Simple - Teacher names",
    question         = "Who are the faculty at Panaversity?",
    expected_path    = "simple",
    should_find_answer = True
)

run_test(
    test_name        = "Simple - CCA-F definition",
    question         = "What does CCA-F stand for?",
    expected_path    = "simple",
    should_find_answer = True
)

run_test(
    test_name        = "Simple - RAG paper fact",
    question         = "What retriever does the RAG paper use?",
    expected_path    = "simple",
    should_find_answer = True
)

run_test(
    test_name        = "Simple - Not in documents",
    question         = "Who is Muhammad Qasim?",
    expected_path    = "simple",
    should_find_answer = False
)


# ================================================================
# COMPLEX PATH TESTS
# These questions should route to complex path
# ================================================================

run_test(
    test_name        = "Complex - Comparison",
    question         = "Compare the Agentic AI Architect Program vs the Agentic AI Business Strategist Program",
    expected_path    = "complex",
    should_find_answer = True
)

run_test(
    test_name        = "Complex - Architecture explanation",
    question         = "Explain the architecture and teaching approach of Panaversity",
    expected_path    = "complex",
    should_find_answer = True
)

run_test(
    test_name        = "Complex - RAG paper deep question",
    question         = "What is the difference between RAG-Sequence and RAG-Token models?",
    expected_path    = "complex",
    should_find_answer = True
)

run_test(
    test_name        = "Complex - Multi step",
    question         = "What technologies does a student learn across all levels at Panaversity?",
    expected_path    = "complex",
    should_find_answer = True
)


# ================================================================
# EDGE CASE TESTS
# ================================================================

run_test(
    test_name        = "Edge - Very short question",
    question         = "What is RAG?",
    expected_path    = "simple",
    should_find_answer = True
)

run_test(
    test_name        = "Edge - Question with no relevant data",
    question         = "What is the weather in Karachi today?",
    expected_path    = "simple",
    should_find_answer = False)


# ================================================================
# RESULTS SUMMARY
# ================================================================

total = passed + failed

print("\n")
print("=" * 50)
print("TEST RESULTS SUMMARY")
print("=" * 50)
print(f"TOTAL  : {total}")
print(f"PASSED : {passed}")
print(f"FAILED : {failed}")
print(f"SCORE  : {round((passed / total) * 100)}% passing")
print("=" * 50)