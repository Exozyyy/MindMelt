export interface TestCase {
    question: string;
    options: string[];
    correct_answer: string;
    explanation: string;
}

export interface TopicData {
    explanation: string;
    test_cases: TestCase[];
}
