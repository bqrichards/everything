import { useEffect, useState } from 'react'
import { LibraryItem } from './components/LibraryItem'
import { Media } from './models/Media'
import './LibraryPage.css'

export const LibraryPage = () => {
	const [media, setMedia] = useState<Media[]>([])

	useEffect(() => {
		fetch('http://127.0.0.1:5000/api/all')
			.then(response => response.json())
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