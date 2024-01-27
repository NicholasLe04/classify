import './App.css';
import CourseSearch from './components/CourseSearch';

function App() {
  return (
    <div className="App">
      <h1 className="Title">Classify</h1>
      <p>
        Enter a prompt with <strong>natural language</strong> and find courses that suit <strong>you</strong>!<br/>
        Try out a prompt such as "I like drawing"!<br/>
        <br/>
        Created by: Nicholas Le
      </p>
      <CourseSearch />
    </div>
  );
}

export default App;
