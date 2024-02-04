import React, { useState } from 'react';
import "./CourseSearch.css";

function CourseSearch() {

  const [loading, setLoading] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  function getRecommendations(limit) {
    if (prompt === "") {
      setRecommendations([])
    }
    else {
      setLoading(true);

      fetch(
        `${process.env.REACT_APP_API_ENDPOINT_BASE}/api/v1/get-courses/`, 
        {
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': process.env.REACT_APP_API_KEY
          },
          body: JSON.stringify({
            "user_query": prompt,
            "limit": limit
          })
        }
      )
      .then(response => response.json())
      .then(content => setRecommendations(content['courses']))
      .then(() => setLoading(false));
    }
  }

  return (
    <div className='course-search'>
      <input 
        id='course-search-bar'
        className={loading ? 'disabled' : ''}
        placeholder='I love to...' 
        type='text'
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !loading) {
            getRecommendations(5);
          }
        }}
      />
      { loading && <p id='loading-text'>Finding your personalized courses...</p> }
      <ul>
        {
          recommendations.map((course) => {
            return (
              <a href={`https://catalog.sjsu.edu/preview_course_nopop.php?catoid=${course.course_data.catoid}&coid=${course.course_data.coid}`} target='__blank'>
                <li>
                  <p className='course-code'>{course.course_code}</p>
                  <p>{course.course_data.course_description}</p>
                </li>
              </a>
            )
          })
        }
        {
          recommendations.length > 0 && 
          <button id='load-more' onClick={() => {
            getRecommendations(recommendations.length + 5)
          }}>
            Load More
          </button>
        }
      </ul>
    </div>
  )
}

export default CourseSearch
