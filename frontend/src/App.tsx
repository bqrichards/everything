import './App.css'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { LibraryPage } from './LibraryPage'

function App() {
	return (
		<Router>
			<Switch>
				<Route path="/">
					<LibraryPage />
				</Route>
			</Switch>
		</Router>
	)
}

export default App
