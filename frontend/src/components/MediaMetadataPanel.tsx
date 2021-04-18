import { FC } from 'react'
import { Media } from '../models/Media'
import { Link } from 'react-router-dom'

interface MediaMetadataPanelProps {
	media?: Media
}

export const MediaMetadataPanel: FC<MediaMetadataPanelProps> = props => (
	<div style={{padding: 16, paddingTop: 0}}>
		<div style={{display: 'flex', flexDirection: 'row', justifyContent: 'flex-end'}}>
			<Link to='/'>
				<div>
					Library
				</div>
			</Link>
		</div>
		<h2>Title</h2>
		<p>{props.media?.title || '(not set)'}</p>
		<h2>Comment</h2>
		<p>{props.media?.comment || '(not set)'}</p>
		<h2>Date &amp; Time</h2>
		<p>{props.media?.date || '(not set)'}</p>
	</div>
)