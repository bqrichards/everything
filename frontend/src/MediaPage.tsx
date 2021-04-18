import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { api, urlFromEndpoint } from './api'
import { MediaMetadataPanel } from './components/MediaMetadataPanel'
import './MediaPage.css'

interface MediaPageParams {
	mediaId: string
}

export const MediaPage = () => {
	const { mediaId } = useParams<MediaPageParams>()

	const [media, setMedia] = useState()

	useEffect(() => {
		api.get(`api/media/${mediaId}`)
			.then(response => response.data)
			.then(setMedia)
			.catch(e => {
				console.warn(e)
			})
	}, [])

	return (
		<div id='media-page-container'>
			<div id='media-page-display-container'>
				<img
					id='media-page-display-image'
					src={urlFromEndpoint(`api/media/visual/${mediaId}`)}
					alt={media?.title || 'Untitled Media'} />
			</div>
			<div id='media-page-edit-panel'>
				<MediaMetadataPanel media={media} />
			</div>
		</div>
	)
}