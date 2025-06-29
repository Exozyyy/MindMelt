import { useAppSelector } from "../../../shared/lib/hooks/Hooks.tsx";

const Quiz = () => {
    const quiz = useAppSelector((state) => state.topic.test_cases);
    const status = useAppSelector((state) => state.topic.status);

    if (status === "loading") return <p>Подгружаем вопросы, не скучай...</p>;
    if (status === "failed") return <p>Что-то пошло не так :(</p>;

    const checkAnswer = (questionIndex: number, optionIndex: number) => {
        // @ts-ignore
        const correctAnswer = quiz[questionIndex].correct_answer || undefined
        const userAnswer = String.fromCharCode(65 + optionIndex);
        if (userAnswer === correctAnswer) {
            alert("Правильно");
        } else {
            alert(`Неправильно, Правильный ответ: ${correctAnswer}`);
        }

    }
    console.log(quiz)

    return (
        <div className="quiz-container max-w-3xl mx-auto p-4">
            <h2 className="text-2xl font-bold mb-6">Вопросы</h2>
            {quiz && quiz.length > 0 ? (
                <ol className="space-y-6 list-decimal list-inside">
                    {quiz.map(({ question, options }, index) => (
                        <li key={index} className="mb-4">
                            <p className="font-semibold mb-2">{question}</p>
                            <ul className="ml-6 list-disc space-y-1">
                                {options.map((option, i) => (
                                    <li key={i}>
                                        <button
                                            onClick={() => checkAnswer(index, i)}
                                            className="hover:underline hover:text-blue-600 transition-colors"
                                        >
                                            {option}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ol>
            ) : (
                <p>Нет доступных вопросов.</p>
            )}
        </div>
    );
};

export default Quiz;
