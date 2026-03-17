import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage

# --- 1. SYSTEM PROMPT & PERSONA ---
# Persona: Juli Rani Das (Nurse, Comilla Sadar Hospital)
# Instructor: Payal Prasad (Medical Assistant, Comilla Midtown Eye Hospital)
SYSTEM_PROMPT = (
    "You are Juli Rani Das, a dedicated Nurse at Comilla Sadar Hospital. "
    "You are currently providing medical reports and assistance based on instructions "
    "from Payal Prasad, a Medical Assistant at Comilla Midtown Eye Hospital. "
    "Your tone should be professional, empathetic, and culturally respectful to the "
    "people of Comilla. Always verify patient names before disclosing report details."
)

# --- 2. ENHANCED TOOLS ---
@tool
def fetch_medical_report(patient_name: str):
    """Retrieves the medical report status for a specific patient."""
    # Mock Database
    reports = {
        "Abdur Rahman": "Blood sugar levels are stable at 110 mg/dL. Vision screening recommended.",
        "Sumaiya Akter": "Post-operative recovery is on track. Follow-up with Payal Prasad at Midtown Eye Hospital next Tuesday.",
        "Kiron Mia": "X-ray results show a minor hairline fracture in the left radius."
    }
    return reports.get(patient_name, f"I'm sorry, I couldn't find a report for {patient_name} in the Comilla Sadar records.")

@tool
def check_inventory(item_name: str):
    """Check if a medical supply or medicine is in stock."""
    inventory = {"insulin": 15, "saline": 50, "eye drops": 20, "paracetamol": 100}
    count = inventory.get(item_name.lower(), 0)
    return f"We have {count} units of {item_name} available in the Sadar Hospital pharmacy."

tools = [fetch_medical_report, check_inventory]
llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)
client = OpenAI() # Ensure OPENAI_API_KEY is in your environment variables

# --- 3. VOICE FUNCTIONS ---
def record_audio(filename="input.wav", duration=5, fs=44100):
    print("🎤 Juli is listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, (recording * 32767).astype(np.int16)) # Convert to 16-bit PCM
    print("✅ Recording captured.")

def transcribe_audio(filename="input.wav"):
    with open(filename, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    return transcript.text

def play_voice(text):
    print(f"👩‍⚕️ Payal Prasad: {text}")
    response = client.audio.speech.create(model="tts-1", voice="nova", input=text)
    response.stream_to_file("output.mp3")
    # Play audio based on OS
    if os.name == 'posix':
        os.system("afplay output.mp3") # Mac
    else:
        os.system("start output.mp3") # Windows

# --- 4. AGENT GRAPH SETUP ---
def chatbot(state: MessagesState):
    # Prepend system prompt to the message history
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", chatbot)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- 5. MAIN EXECUTION LOOP ---
def run_voice_bot():
    print("--- Medical Agent Active (Juli Rani Das & Payal Prasad) ---")
    print("Press Ctrl+C to exit.")
    
    # Initialize state with a greeting from Juli
    state = {"messages": []}
    
    while True:
        try:
            record_audio()
            user_text = transcribe_audio()
            print(f"👤 Patient/Staff: {user_text}")
            
            # Update state and invoke graph
            state["messages"].append(HumanMessage(content=user_text))
            result = app.invoke(state)
            
            # Update history and speak the last AI message
            state["messages"] = result["messages"]
            final_response = result["messages"][-1].content
            play_voice(final_response)
            
        except KeyboardInterrupt:
            print("\nShutting down medical assistant...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_voice_bot()