import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {postTopicData} from "../api/topicApi.tsx"
import type {TopicData} from '../types/types';

export const fetchTopic = createAsyncThunk(
    "topic/fetchTopic",
    async (topic: string) => {
        return await postTopicData<TopicData>(topic);
    }
);

interface ExplanationState {
    value: string;
    explanation: TopicData | null;
    test_cases?: TopicData["test_cases"];
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error: string | null;
}
const initialState: ExplanationState  = {
    value: "",
    explanation: null,
    status: 'idle',
    error: null,
    test_cases: undefined
};


const topicSlice = createSlice({
    name: "topic",
    initialState,
    reducers: {
        setTopic(state, action) {
            state.value = action.payload;
        },
        clearTopic: (state) => {
            state.value = "";
        }
    },
        extraReducers: (builder) => {
            builder
                .addCase(fetchTopic.pending, (state) => {
                    state.status = 'loading';
                })
                .addCase(fetchTopic.fulfilled, (state, action) => {
                    state.status = 'succeeded';
                    state.explanation = action.payload;
                    state.test_cases = action.payload.test_cases;
                })
                .addCase(fetchTopic.rejected, (state) => {
                    state.status = 'failed';
                    // state.error = action.error.message;
                });
        },
},
)

export const { setTopic, clearTopic } = topicSlice.actions;
export default topicSlice.reducer;