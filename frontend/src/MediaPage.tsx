import './MediaPage.css'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router'
import { api, urlFromEndpoint } from './api'
import { MediaMetadataPanel } from './components/MediaMetadataPanel'
import { mediaIsEqual } from './utilities/MediaUtilities'

interface MediaPageParams {
	mediaId: string
}

export const MediaPage = () => {
	const { mediaId } = useParams<MediaPageParams>()

	const [media, setMedia] = useState()
	const [pendingMedia, setPendingMedia] = useState()

	const differs = useMemo(() => mediaIsEqual(media, pendingMedia), [media, pendingMedia])

	useEffect(() => {
		api
			.get(`media/${mediaId}`)
			.then(response => response.data)
			.then(media => {
				setMedia(media)
				setPendingMedia(media)
			})
			.catch(console.warn)
	}, [mediaId])

	const save = useCallback(() => {
		api
			.patch(`media/${mediaId}/edit`, pendingMedia)
			.then(response => response.data)
			.then(console.log)
			.catch(console.warn)
	}, [pendingMedia, mediaId])

	return (
		<div id='media-page-container'>
			<div id='media-page-display-container'>
				<img
					id='media-page-display-image'
					src={urlFromEndpoint(`media/visual/${mediaId}`)}
					alt={media?.title || 'Untitled Media'} />
			</div>
			<div id='media-page-edit-panel'>
				<MediaMetadataPanel media={media} showSaveButton={differs} save={save} />
			</div>
		</div>
	)
}