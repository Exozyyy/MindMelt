import { useAppSelector } from "../../shared/lib/hooks/Hooks.tsx";
import Quiz from "../../features/quiz/ui/Quiz.tsx";

const ExplanationView = () => {
    const explanation = useAppSelector((state) => state.topic.explanation);
    const status = useAppSelector((state) => state.topic.status);

    if (status === 'loading') return <p>Подгружаем, не скучай...</p>;
    if (status === 'failed') return <p>Что-то пошло не так :(</p>;

    return (
        <div className="explanation-container" style={{ animation: 'fadeIn 0.5s ease forwards' }}>
            <h2 className="text-xl font-bold">Объяснение</h2>
            {explanation && <p style={{ whiteSpace: 'pre-wrap' }}>{explanation.explanation}</p>}
            <Quiz />
        </div>
    );
};

export default ExplanationView;
