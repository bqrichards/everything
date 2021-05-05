import { FC } from 'react'
import { urlFromEndpoint } from '../api'
import { Media } from '../models/Media'
import './LibraryItem.css'

interface LibraryItemProps {
	media: Media
}

export const LibraryItem: FC<LibraryItemProps> = props => (
	<div className='LibraryItem grid-item'>
		<img
			className='LibraryItemImage'
			src={urlFromEndpoint(`thumbnail/${props.media.id}`)}
			alt='' />
	</div>
)