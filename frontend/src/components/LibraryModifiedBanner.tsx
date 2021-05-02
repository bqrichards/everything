import { FC } from 'react'

interface LibraryModifiedBannerProps {
	writeChanges: () => void
}

export const LibraryModifiedBanner: FC<LibraryModifiedBannerProps> = props => (
	<div style={{backgroundColor: '#6495ED', padding: 12, borderRadius: 12}}>
		<span style={{color: 'white', marginRight: 32}}>Modified</span>
		<button onClick={props.writeChanges}>Write Changes</button>
	</div>
)