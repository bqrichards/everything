import { FC } from 'react'

interface AddMediaFileRowProps {
	file: File
}

export const AddMediaFileRow: FC<AddMediaFileRowProps> = ({ file }) => (
	<div style={{marginTop: 8, marginBottom: 8}}>
		{file.name}
	</div>
)
