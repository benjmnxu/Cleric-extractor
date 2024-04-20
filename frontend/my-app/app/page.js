"use client";
require("dotenv").config({ path: "../.env" });

import React, { useState, useEffect, useRef } from "react";

export default function Home() {
  const containerRef = useRef(null);

  const [question, setQuestion] = useState("");
  const [urls, setUrls] = useState([""]);
  const [summary, setSummary] = useState("");

  useEffect(() => {
    containerRef.current.scrollTop = containerRef.current.scrollHeight;
  }, [urls]);

  const pollForStatus = async () => {
    try {
      let status = "processing";
      while (status !== "done") {
        console.log("polling");
        const response = await fetch(
          process.env.NEXT_PUBLIC_DOMAIN_URL + "/get_question_and_facts"
        );
        const data = await response.json();
        status = data.status;
        if (status === "done") {
          setSummary(data.facts);
          break;
        }
        await new Promise((resolve) => setTimeout(resolve, 2500));
      }
    } catch (error) {
      console.error("Error polling for status:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      console.log(process.env);
      console.log(process.env.DOMAIN_URL);
      const response = await fetch(
        process.env.NEXT_PUBLIC_DOMAIN_URL + "/submit_question_and_documents",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
            documents: urls,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(response.status);
      }

      console.log("Form submitted successfully");

      pollForStatus();
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  const displaySummary = () => {
    if (summary && summary.length > 0) {
      return (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {summary.map((item, index) => (
            <li
              key={index}
              style={{
                listStyleType: "none",
                paddingLeft: "1em",
                textIndent: "-1em",
                marginBottom: "0.5em",
              }}
            >
              <span style={{ color: "black", marginRight: "8px" }}>•</span>
              {item}
            </li>
          ))}
        </ul>
      );
    }
    return null;
  };

  const handleChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleUrlChange = (index, value) => {
    const updatedUrls = [...urls];
    updatedUrls[index] = value;
    setUrls(updatedUrls);
  };

  const handleAddUrl = () => {
    setUrls([...urls, ""]);
  };

  const handleDeleteUrl = (index) => {
    const updatedUrls = [...urls];
    updatedUrls.splice(index, 1);
    setUrls(updatedUrls);
  };

  return (
    <div className="bg-black">
      <h1 className="text-4xl font-bold mt-10 text-slate-100 text-center">
        Extractor
      </h1>
      <div className="mx-auto w-10/12 mt-7">
        <input
          type="text"
          name="fieldName"
          value={question}
          onChange={handleChange}
          className="block w-full px-4 py-2 rounded-lg text-black bg-slate-100"
          placeholder="Question"
        />
      </div>
      <div className="flex mx-auto w-10/12">
        <div className="w-3/12 h-5/6 bg-gray-100 rounded-lg p-4 mt-4 mr-4 self-start">
          <h2 className="text-black mb-2">Logs</h2>
          <div ref={containerRef} className="h-80 overflow-y-scroll">
            {urls.map((url, index) => (
              <div key={index} className="flex items-center">
                <input
                  key={index}
                  type="text"
                  value={url}
                  onChange={(e) => handleUrlChange(index, e.target.value)}
                  className="w-full px-4 py-2 rounded-lg text-black mt-4"
                  placeholder="Enter URL"
                />
                <button
                  onClick={() => handleDeleteUrl(index)}
                  className="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 focus:outline-none focus:bg-red-600 ml-2 mt-4"
                >
                  X
                </button>
              </div>
            ))}
          </div>

          <div className="flex justify-center">
            <button
              onClick={handleAddUrl}
              className="sticky mt-2 w-9/12 bg-slate-100 text-black px-3 py-1 border border-black rounded-md hover:bg-slate-200 focus:outline-none focus:bg-slate-200"
            >
              Add URL
            </button>
          </div>
        </div>
        <div className="w-9/12 h-96 bg-gray-100 rounded-lg p-4 mt-4 ml-4">
          <h2 className="text-black mb-2">Log Summary</h2>
          <div className="w-full px-4 py-2 rounded-lg text-black mt-4">
            {displaySummary()}
          </div>
        </div>
      </div>
      <div className="mt-5 ml-32">
        <button
          type="submit"
          className="block bg-slate-100 text-black px-4 py-2 rounded-md hover:bg-slate-200 focus:outline-none focus:bg-slate-200"
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
    </div>
  );
}
