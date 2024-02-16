let DID_API; // Declare the variable outside the promise chain

async function fetchApiData() {
  try {
    const response = await fetch("static/api.json");
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

      // Continue your application logic here
      const sessionResponse = await fetch(`${DID_API.url}/talks/streams`, {
        method: "POST",
        headers: {
          Authorization: `Basic ${DID_API.key}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          source_url:
            "https://raw.githubusercontent.com/jjmlovesgit/D-id_Streaming_Chatgpt/main/oracle_pic.jpg",
        }),
      });
      
      // Return sessionResponse from the function
      return sessionResponse;
    }
  } catch (error) {
    console.error("Error loading API:", error);
    throw error; // Optionally rethrow the error
  }
}

// Call the async function
fetchApiData()
  .then(sessionResponse => {
    // Process sessionResponse further if needed
    console.log("Session response:", sessionResponse);
  })
  .catch(error => {
    // Handle errors from the async function
    console.error("Error fetching API data:", error);
  });


  const fetchApiData = async () => {
    let DID_API; // Declare DID_API as a local variable
    try {
      const response = await fetch("static/api.json");
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
  
        // You can continue your application logic here
      }
    } catch (error) {
      console.error("Error loading API:", error);
    }
    return DID_API; // Return DID_API from the function
  };
  
  // Define DID_API constant and assign the value returned by fetchApiData
  const DID_API = await fetchApiData();
  
  // Now you can use DID_API constant throughout your code
  console.log(DID_API);
  