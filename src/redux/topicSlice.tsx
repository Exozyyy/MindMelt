import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL} from "../config.ts";

export const fetchTopic = createAsyncThunk(
    "topic/fetchTopic",
    async (topic: string) => {
        const response = await fetch(`${API_URL}explain-topic`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic })
        });

        if (!response.ok) {
            throw new Error("Failed to fetch topic");
        }
        const data = await response.json();
        return data;
    }
);

interface ExplanationData {
    explanation: string;
    test_case: string;
}

interface TopicState {
    value: string;
    explanation: ExplanationData | null;
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error: string | null;
}
const initialState: TopicState = {
    value: "",
    explanation: null,
    status: 'idle',
    error: null,
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