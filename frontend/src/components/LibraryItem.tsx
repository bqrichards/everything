import { FC } from 'react'
import { Media } from '../models/Media'
import './LibraryItem.css'

interface LibraryItemProps {
	media: Media
}

export const LibraryItem: FC<LibraryItemProps> = props => (
	<div className='LibraryItem grid-item'>
		<img
			className='LibraryItemImage'
			src={`api/thumbnail/${props.media.id}`}
			alt={props.media.title} />
	</div>
)