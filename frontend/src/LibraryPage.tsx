import { useEffect, useState } from 'react'
import { LibraryItem } from './components/LibraryItem'
import { Media } from './models/Media'
import { api } from './api'
import { Link } from 'react-router-dom'
import './LibraryPage.css'

export const LibraryPage = () => {
	const [media, setMedia] = useState<Media[]>([])

	useEffect(() => {
		api.get<Media[]>('api/all')
			.then(response => response.data)
			.then(setMedia)
			.catch(e => {
				console.warn(e)
			})
	}, [])

	return (
		<div id='library-page-container'>
			<h1>Library</h1>
			<div className='grid-container'>
				{media.map(mediaItem => (
					<Link to={`/media/${mediaItem.id}`}>
						<LibraryItem
							key={String(mediaItem.id)}
							media={mediaItem} />
					</Link>
				))}
			</div>
		</div>
	)
}