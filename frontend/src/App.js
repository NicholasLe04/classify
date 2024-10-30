import './App.css';
import CourseSearch from './components/CourseSearch';

function App() {
  return (
    <div className="App">
      <h1 className="Title">Classify</h1>
      <p>
        Enter a prompt with <strong>natural language</strong> and find related courses at SJSU!
        <br/>
        Try out a prompt such as "that one game where you put the ball in the hoop"!
        <br/>
        <br/>
        Created by: Nicholas Le
      </p>
      <CourseSearch />
    </div>
  );
}

export default App;
