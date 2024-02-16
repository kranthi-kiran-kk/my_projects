// const config = require('static\\config.json');

let OPENAI_API_KEY;

async function loadConfig() {
    try {
        const response = await fetch("static\\config.json");
        const config = await response.json();
        OPENAI_API_KEY = config.OPENAI_API_KEY;
    } catch (error) {
        console.error("Error loading config.json:", error);
    }
}

const OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions";


async function fetchOpenAIResponse(userMessage) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [{role: "user", content: userMessage}],
        temperature: 0.7,
        max_tokens: 25
      }),
    });
    
    if (!response.ok) {
      throw new Error(`OpenAI API request failed with status ${response.status}`);
    }
    const data = await response.json();
    return data.choices[0].message.content.trim();
  }

  async function main() {
    await loadConfig();

    const userInput = "Who is the CEO of Tesla?";
    const openAIResponse = await fetchOpenAIResponse(userInput);

    console.log("User Input:", userInput);
    console.log("OpenAI Response:", openAIResponse);
}

// const userInput = "Who is the CEO of Tesla?";
// const openAIResponse = await fetchOpenAIResponse(userInput);

// console.log("User Input:", userInput);
// console.log("OpenAI Response:", openAIResponse);

main().catch((error) => console.error(error));
