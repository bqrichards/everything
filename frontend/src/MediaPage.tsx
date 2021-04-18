import { useParams } from 'react-router'

export const MediaPage = () => {
	const { mediaId } = useParams()

	return (
		<div>
			<p>Media ID: {mediaId}</p>
		</div>
	)
}