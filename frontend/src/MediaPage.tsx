import './MediaPage.css'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router'
import { api, urlFromEndpoint } from './api'
import { MediaChangedFunction, MediaMetadataPanel } from './components/MediaMetadataPanel'
import { initMedia, mediaIsEqual } from './utilities/MediaUtilities'
import { Media } from './models/Media'
import moment from 'moment'

interface MediaPageParams {
	mediaId: string
}

export const MediaPage = () => {
	const { mediaId } = useParams<MediaPageParams>()

	const [media, setMedia] = useState<Media>()
	const [pendingMedia, setPendingMedia] = useState<Media>()

	const differs = useMemo(() => !mediaIsEqual(media, pendingMedia), [media, pendingMedia])

	useEffect(() => {
		api
			.get(`media/${mediaId}`)
			.then(response => response.data)
			.then(media => {
				// Convert media date to localtime
				media = initMedia(media)
				
				setMedia(media)
				setPendingMedia(media)
			})
			.catch(console.warn)
	}, [mediaId])

	const save = useCallback(() => {
		api
			.patch(`media/${mediaId}/edit`, pendingMedia)
			.then(response => response.data)
			.then(media => {
				media = initMedia(media)
				setMedia(media)
				setPendingMedia(media)
			})
			.catch(console.warn)
	}, [pendingMedia, mediaId])

	const mediaChanged: MediaChangedFunction = useCallback((key, value) => {
		setPendingMedia(oldMedia => {
			const newMedia = {...oldMedia}
			if (key === 'date') {
				// Convert local time to UTC
				newMedia[key] = moment(value).toISOString()
			} else {
				newMedia[key] = value
			}

			return newMedia
		})
	}, [])

	return (
		<div id='media-page-container'>
			<div id='media-page-display-container'>
				<img
					id='media-page-display-image'
					src={urlFromEndpoint(`media/visual/${mediaId}`)} />
			</div>
			<div id='media-page-edit-panel'>
				<MediaMetadataPanel
					media={media}
					mediaChanged={mediaChanged}
					showSaveButton={differs}
					save={save} />
			</div>
		</div>
	)
}