import { useCallback, useEffect, useState } from 'react'
import { LibraryItem } from './components/LibraryItem'
import { LibraryModel } from './models'
import { api } from './api'
import { Link } from 'react-router-dom'
import './LibraryPage.css'
import { LibraryModifiedBanner } from './components/LibraryModifiedBanner'

export const LibraryPage = () => {
	const [library, setLibrary] = useState<LibraryModel>({media: [], canFlush: false})

	useEffect(() => {
		api.get<LibraryModel>('library')
			.then(response => response.data)
			.then(setLibrary)
			.catch(e => {
				console.warn(e)
			})
	}, [])

	const writeChanges = useCallback(() => {
		api.get('flush')
			.then(() => {
				setLibrary(prev => ({...prev, canFlush: false}))
			})
			.catch(e => {
				console.warn(e)
			})
	}, [])

	return (
		<div id='library-page-container'>
			<h1>Library</h1>
			{library.canFlush && <LibraryModifiedBanner writeChanges={writeChanges} />}
			<div className='grid-container'>
				{library.media.map(mediaItem => (
					<Link to={`/media/${mediaItem.id}`} key={String(mediaItem.id)}>
						<LibraryItem media={mediaItem} />
					</Link>
				))}
			</div>
		</div>
	)
}