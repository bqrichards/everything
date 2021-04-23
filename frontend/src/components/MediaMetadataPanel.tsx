import { FC } from 'react'
import { Media } from '../models/Media'
import { Link } from 'react-router-dom'

export type MediaChangedFunction = (key: 'title' | 'comment' | 'date', value: string) => void

interface MediaMetadataPanelProps {
	media?: Media

	/** Callback fired when value of media is edited */
	mediaChanged: MediaChangedFunction

	showSaveButton: boolean

	/** Callback fired when save button is pressed */
	save: () => void
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
		<input
			type='text'
			defaultValue={props.media?.title}
			onChange={e => props.mediaChanged('title', e.target.value)} />
		<h2>Comment</h2>
		<textarea
			rows={3}
			cols={30}
			defaultValue={props.media?.comment}
			onChange={e => props.mediaChanged('comment', e.target.value)} />
		<h2>Date &amp; Time</h2>
		<input
			type='datetime-local'
			defaultValue={props.media?.date || undefined}
			onChange={e => props.mediaChanged('date', e.target.value)} />
		<br /><br /><br />
		{props.showSaveButton && (
			<button onClick={props.save}>Save</button>
		)}
	</div>
)