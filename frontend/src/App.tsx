import './App.css'
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import { LibraryPage } from './LibraryPage'
import { ParentMediaPage } from './ParentMediaPage'

function App() {
	return (
		<BrowserRouter>
			<Switch>
				<Route exact path='/' component={LibraryPage} />
				<Route path='/media' component={ParentMediaPage} />
			</Switch>
		</BrowserRouter>
	)
}

export default App
