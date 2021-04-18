import { FC } from 'react'
import { Media } from '../models/Media'

interface MediaMetadataPanelProps {
	media?: Media
}

export const MediaMetadataPanel: FC<MediaMetadataPanelProps> = props => (
	<div style={{padding: 16, paddingTop: 0}}>
		<h2>Title</h2>
		<p>{props.media?.title || '(not set)'}</p>
		<h2>Comment</h2>
		<p>{props.media?.comment || '(not set)'}</p>
		<h2>Date &amp; Time</h2>
		<p>{props.media?.date || '(not set)'}</p>
	</div>
)