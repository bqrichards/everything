import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Modal from 'react-modal'
import { LibraryItem } from './components/LibraryItem'
import { LibraryModel } from './models'
import { api } from './api'
import { LibraryModifiedBanner } from './components/LibraryModifiedBanner'
import { AddMediaModal } from './components/AddMediaModal'
import './LibraryPage.css'

// TODO
// Modal.setAppElement('#app')

export const LibraryPage = () => {
	const [library, setLibrary] = useState<LibraryModel>({media: [], canFlush: false})
	const [addMediaModalVisible, setAddMediaModalVisible] = useState(false)

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
			<Modal isOpen={addMediaModalVisible} onRequestClose={() => setAddMediaModalVisible(false)}>
				<AddMediaModal />
			</Modal>
			<div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
				<h1>Library</h1>
				<div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', marginRight: 32}}>
					<button onClick={() => setAddMediaModalVisible(true)}>Add Media</button>
				</div>
			</div>
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