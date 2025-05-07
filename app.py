import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)

# 専門家の種類とプロンプトテンプレート
expert_prompts = {
    "心理学者": "あなたは心理学の専門家です。以下の質問に心理学的な観点から答えてください。\n\n質問：{input}",
    "栄養士": "あなたは栄養学の専門家です。以下の質問に栄養学的な観点から答えてください。\n\n質問：{input}",
    "睡眠コンサルタント": "あなたは睡眠の専門家です。以下の質問に睡眠改善の観点から答えてください。\n\n質問：{input}"
}

# LLMにプロンプトを渡して回答を得る関数
def get_llm_response(input_text, expert_type):
    prompt_template = PromptTemplate(template=expert_prompts[expert_type], input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run({"input": input_text})

# StreamlitアプリのUI
st.title("専門家に質問できるアプリ")
st.write("以下のフォームに質問を入力し、専門家の種類を選択して送信してください。")

# 入力フォームとラジオボタン
input_text = st.text_input("質問を入力してください：", "")
expert_type = st.radio("専門家の種類を選択してください：", list(expert_prompts.keys()))

# 送信ボタン
if st.button("送信"):
    if input_text.strip():
        with st.spinner("回答を生成中..."):
            response = get_llm_response(input_text, expert_type)
        st.success("以下が専門家からの回答です：")
        st.write(response)
    else:
        st.error("質問を入力してください。")


