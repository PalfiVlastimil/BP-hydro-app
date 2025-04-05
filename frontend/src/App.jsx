import './App.css';
import Wrapper from './components/Wrapper.jsx';
//import { AuthProvider } from './providers/AuthProvider';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

/**
 *  Start of a Hydroponics application
 * @returns rendered web application
 */
function App() {
  return (
    <div>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <BrowserRouter>
          <Wrapper />
        </BrowserRouter>
      </ThemeProvider>

    </div>
  );
}

export default App;