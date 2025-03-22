import './App.css';
import Wrapper  from './components/Wrapper.jsx';
//import { AuthProvider } from './providers/AuthProvider';
import { BrowserRouter } from 'react-router-dom';
/**
 *  Start of a Hydroponics application
 * @returns rendered web application
 */
function App() {
  return (
    <div>
      <BrowserRouter>
        <Wrapper />
      </BrowserRouter>

    </div>
  );
}

export default App;