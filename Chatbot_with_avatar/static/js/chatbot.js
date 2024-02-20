// Async function to fetch D-id API Key
async function fetchApiData() {
  try {
    const response = await fetch("static\\api.json");
    if (!response.ok) {
      const message = `An error has occured: ${response.status}`;
      throw new Error(message);
    }
    const data = await response.json();

    // Check if the API key exists and is valid
    if (data && data.key === "key") {
      alert("Please put your API key inside api.json and restart.");
    } else {
      // If the API key is valid, continue with the application logic
      DID_API = data;
      // Use the API key and URL
      console.log("API key:", DID_API.key);
      console.log("API URL:", DID_API.url);
    }
  } catch (error) {
    console.error("Error loading API:", error);
  }
  return DID_API;
}

// Async function to  fetch GPT API key
async function fetchConfig() {
  try {
    const response = await fetch("static\\config.json");
    const config = await response.json();
    OPENAI_API_KEY = config.OPENAI_API_KEY;
    return OPENAI_API_KEY;
  } catch (error) {
    console.error("Error loading config.json:", error);
  }
}

// OpenAI API endpoint
async function fetchOpenAIResponse(userMessage) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: userMessage }],
      temperature: 0.7,
      max_tokens: 25,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenAI API request failed with status ${response.status}`);
  }
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// langchain-custom-chat API endpoint
async function fetchlangchainResponse(userMessage) {
  try{
    const response = await fetch("/answer", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({userquery:userMessage}),
      });

      const data = await response.json();
      return data.answer;
  }catch (error) {
    console.error('There was a problem with your fetch operation:', error);
  }
  }
 

const RTCPeerConnection = (
  window.RTCPeerConnection ||
  window.webkitRTCPeerConnection ||
  window.mozRTCPeerConnection
).bind(window);

let peerConnection;
let streamId;
let sessionId;
let sessionClientAnswer;

let statsIntervalId;
let videoIsPlaying;
let lastBytesReceived;

const talkVideo = document.getElementById("talk-video");
talkVideo.setAttribute("playsinline", "");
const peerStatusLabel = document.getElementById("peer-status-label");
const iceStatusLabel = document.getElementById("ice-status-label");
const iceGatheringStatusLabel = document.getElementById(
  "ice-gathering-status-label"
);
const signalingStatusLabel = document.getElementById("signaling-status-label");
const streamingStatusLabel = document.getElementById("streaming-status-label");

const connectButton = document.getElementById("connect-button");
connectButton.onclick = async () => {
  if (peerConnection && peerConnection.connectionState === "connected") {
    return;
  }

  stopAllStreams();
  closePC();

  const DID_API = await fetchApiData();

  const sessionResponse = await fetch(`${DID_API.url}/talks/streams`, {
    method: "POST",
    headers: {
      Authorization: `Basic ${DID_API.key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      source_url:
        "https://raw.githubusercontent.com/kranthi-kiran-kk/my_projects/main/Chatbot_with_avatar/static/saleswoman2.jpg",
    }),
  });

  const {
    id: newStreamId,
    offer,
    ice_servers: iceServers,
    session_id: newSessionId,
  } = await sessionResponse.json();
  streamId = newStreamId;
  sessionId = newSessionId;

  console.log(streamId, sessionId);

  try {
    sessionClientAnswer = await createPeerConnection(offer, iceServers);
  } catch (e) {
    console.log("error during streaming setup", e);
    stopAllStreams();
    closePC();
    return;
  }

  const sdpResponse = await fetch(
    `${DID_API.url}/talks/streams/${streamId}/sdp`,
    {
      method: "POST",
      headers: {
        Authorization: `Basic ${DID_API.key}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        answer: sessionClientAnswer,
        session_id: sessionId,
      }),
    }
  );
};

// responseFromOpenAI
const talkButton = document.getElementById("talk-button");
talkButton.onclick = async () => {
  if (
    peerConnection?.signalingState === "stable" ||
    peerConnection?.iceConnectionState === "connected"
  ) {
    const chatbot = document.getElementById("chatbot");
    const conversation = document.getElementById("conversation");
    const inputForm = document.getElementById("input-form");
    // await fetchConfig();
    const userInput = document.getElementById("input-field").value;
    // const responseFromOpenAI = await fetchOpenAIResponse(userInput);
    const responseFromLangchain = await fetchlangchainResponse(userInput)

    // Print the openAIResponse to the console
    // console.log("OpenAI Response:", responseFromOpenAI);
    console.log("Langchain Response:", responseFromLangchain);

    // Clear input field
    document.getElementById("input-field").value = "";
    const currentTime = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // Add user input to conversation
    let message = document.createElement("div");
    message.classList.add("chatbot-message", "user-message");
    message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${userInput}</p>`;
    conversation.appendChild(message);

    // Add chatbot response to conversation
    message = document.createElement("div");
    message.classList.add("chatbot-message", "chatbot");
    // message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${responseFromOpenAI}</p>`;
    message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${responseFromLangchain}</p>`;
    conversation.appendChild(message);
    message.scrollIntoView({ behavior: "smooth" });

    // const DID_API = await fetchApiData();

    // const talkResponse = await fetch(
    //   `${DID_API.url}/talks/streams/${streamId}`,
    //   {
    //     method: "POST",
    //     headers: {
    //       Authorization: `Basic ${DID_API.key}`,
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       script: {
    //         type: "text",
    //         subtitles: "false",
    //         provider: {
    //           type: "microsoft",
    //           voice_id: "en-US-AmberNeural",
    //         },
    //         ssml: false,
    //         input: responseFromOpenAI, //send the openAIResponse to D-id
    //       },
    //       config: {
    //         fluent: true,
    //         pad_audio: 0,
    //         driver_expressions: {
    //           expressions: [
    //             { expression: "neutral", start_frame: 0, intensity: 0 },
    //           ],
    //           transition_frames: 0,
    //         },
    //         align_driver: true,
    //         align_expand_factor: 0,
    //         auto_match: true,
    //         motion_factor: 0,
    //         normalization_factor: 0,
    //         sharpen: true,
    //         stitch: true,
    //         result_format: "mp4",
    //       },
    //       driver_url: "bank://lively/",
    //       config: {
    //         stitch: true,
    //       },
    //       session_id: sessionId,
    //     }),
    //   }
    // );
  }
};

const destroyButton = document.getElementById("destroy-button");
destroyButton.onclick = async () => {
  const DID_API = await fetchApiData();
  await fetch(`${DID_API.url}/talks/streams/${streamId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Basic ${DID_API.key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ session_id: sessionId }),
  });

  stopAllStreams();
  closePC();
};

function onIceGatheringStateChange() {
  iceGatheringStatusLabel.innerText = peerConnection.iceGatheringState;
  iceGatheringStatusLabel.className =
    "iceGatheringState-" + peerConnection.iceGatheringState;
}

function onIceCandidate(event) {
  console.log("onIceCandidate", event);
  if (event.candidate) {
    const { candidate, sdpMid, sdpMLineIndex } = event.candidate;

    fetch(`${DID_API.url}/talks/streams/${streamId}/ice`, {
      method: "POST",
      headers: {
        Authorization: `Basic ${DID_API.key}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        candidate,
        sdpMid,
        sdpMLineIndex,
        session_id: sessionId,
      }),
    });
  }
}

function onIceConnectionStateChange() {
  iceStatusLabel.innerText = peerConnection.iceConnectionState;
  iceStatusLabel.className =
    "iceConnectionState-" + peerConnection.iceConnectionState;
  if (
    peerConnection.iceConnectionState === "failed" ||
    peerConnection.iceConnectionState === "closed"
  ) {
    stopAllStreams();
    closePC();
  }
}

function onConnectionStateChange() {
  // not supported in firefox
  peerStatusLabel.innerText = peerConnection.connectionState;
  peerStatusLabel.className =
    "peerConnectionState-" + peerConnection.connectionState;
}

function onSignalingStateChange() {
  signalingStatusLabel.innerText = peerConnection.signalingState;
  signalingStatusLabel.className =
    "signalingState-" + peerConnection.signalingState;
}

function onVideoStatusChange(videoIsPlaying, stream) {
  let status;
  if (videoIsPlaying) {
    status = "streaming";
    const remoteStream = stream;
    setVideoElement(remoteStream);
  } else {
    status = "empty";
    playIdleVideo();
  }
  streamingStatusLabel.innerText = status;
  streamingStatusLabel.className = "streamingState-" + status;
}

function onTrack(event) {
  if (!event.track) return;

  statsIntervalId = setInterval(async () => {
    const stats = await peerConnection.getStats(event.track);
    stats.forEach((report) => {
      if (report.type === "inbound-rtp" && report.mediaType === "video") {
        const videoStatusChanged =
          videoIsPlaying !== report.bytesReceived > lastBytesReceived;

        if (videoStatusChanged) {
          videoIsPlaying = report.bytesReceived > lastBytesReceived;
          onVideoStatusChange(videoIsPlaying, event.streams[0]);
        }
        lastBytesReceived = report.bytesReceived;
      }
    });
  }, 500);
}

async function createPeerConnection(offer, iceServers) {
  if (!peerConnection) {
    peerConnection = new RTCPeerConnection({ iceServers });
    peerConnection.addEventListener(
      "icegatheringstatechange",
      onIceGatheringStateChange,
      true
    );
    peerConnection.addEventListener("icecandidate", onIceCandidate, true);
    peerConnection.addEventListener(
      "iceconnectionstatechange",
      onIceConnectionStateChange,
      true
    );
    peerConnection.addEventListener(
      "connectionstatechange",
      onConnectionStateChange,
      true
    );
    peerConnection.addEventListener(
      "signalingstatechange",
      onSignalingStateChange,
      true
    );
    peerConnection.addEventListener("track", onTrack, true);
  }

  await peerConnection.setRemoteDescription(offer);
  console.log("set remote sdp OK");

  const sessionClientAnswer = await peerConnection.createAnswer();
  console.log("create local sdp OK");

  await peerConnection.setLocalDescription(sessionClientAnswer);
  console.log("set local sdp OK");

  return sessionClientAnswer;
}

function setVideoElement(stream) {
  if (!stream) return;
  talkVideo.srcObject = stream;
  talkVideo.loop = false;

  // safari hotfix
  if (talkVideo.paused) {
    talkVideo
      .play()
      .then((_) => {})
      .catch((e) => {});
  }
}

function playIdleVideo() {
  talkVideo.srcObject = undefined;
  talkVideo.src = "static\\saleswomen-idle.mp4";
  talkVideo.loop = true;
}

function stopAllStreams() {
  if (talkVideo.srcObject) {
    console.log("stopping video streams");
    talkVideo.srcObject.getTracks().forEach((track) => track.stop());
    talkVideo.srcObject = null;
  }
}

function closePC(pc = peerConnection) {
  if (!pc) return;
  console.log("stopping peer connection");
  pc.close();
  pc.removeEventListener(
    "icegatheringstatechange",
    onIceGatheringStateChange,
    true
  );
  pc.removeEventListener("icecandidate", onIceCandidate, true);
  pc.removeEventListener(
    "iceconnectionstatechange",
    onIceConnectionStateChange,
    true
  );
  pc.removeEventListener(
    "connectionstatechange",
    onConnectionStateChange,
    true
  );
  pc.removeEventListener("signalingstatechange", onSignalingStateChange, true);
  pc.removeEventListener("track", onTrack, true);
  clearInterval(statsIntervalId);
  iceGatheringStatusLabel.innerText = "";
  signalingStatusLabel.innerText = "";
  iceStatusLabel.innerText = "";
  peerStatusLabel.innerText = "";
  console.log("stopped peer connection");
  if (pc === peerConnection) {
    peerConnection = null;
  }
}

const maxRetryCount = 3;
const maxDelaySec = 4;
async function fetchWithRetries(url, options, retries = 3) {
  try {
    return await fetch(url, options);
  } catch (err) {
    if (retries <= maxRetryCount) {
      const delay =
        Math.min(Math.pow(2, retries) / 4 + Math.random(), maxDelaySec) * 1000;

      await new Promise((resolve) => setTimeout(resolve, delay));

      console.log(
        `Request failed, retrying ${retries}/${maxRetryCount}. Error ${err}`
      );
      return fetchWithRetries(url, options, retries + 1);
    } else {
      throw new Error(`Max retries exceeded. error: ${err}`);
    }
  }
}
