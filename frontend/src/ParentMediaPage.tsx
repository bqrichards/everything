import { Switch, Route, useRouteMatch, Link } from 'react-router-dom'
import { MediaPage } from './MediaPage'

export const ParentMediaPage = () => {
	const match = useRouteMatch()

	return (
		<Switch>
			<Route path={`${match.path}/:mediaId`} component={MediaPage} />
			<Route path={match.path}>
				<div>
					<h3>Whoops! How did you get here?</h3>
					<Link to='/'>Return to Library</Link>
				</div>
			</Route>
		</Switch>
	)
}