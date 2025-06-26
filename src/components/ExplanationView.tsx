import { useAppSelector } from "../redux/Hooks";

const ExplanationView = () => {
    const explanation = useAppSelector((state) => state.topic.explanation);
    const status = useAppSelector((state) => state.topic.status);

    if (status === 'loading') return <p>Подгружаем, не скучай...</p>;
    if (status === 'failed') return <p>Что-то пошло не так :(</p>;

    return (
        <div className="explanation-container">
            <h2 className="text-xl font-bold">Объяснение</h2>
                {explanation && <p>{explanation.explanation}</p>}
        </div>
    );
};
export default ExplanationView;