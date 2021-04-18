import { useEffect, useState } from 'react'
import { LibraryItem } from './components/LibraryItem'
import { Media } from './models/Media'
import { api } from './api'
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
				{media.map(mediaItem => <LibraryItem key={String(mediaItem.id)} media={mediaItem} />)}
			</div>
		</div>
	)
}