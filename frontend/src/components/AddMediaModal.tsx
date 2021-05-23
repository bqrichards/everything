import { useCallback, useRef, useState } from 'react'
import { urlFromEndpoint } from '../api'
import { AddMediaFileRow } from './AddMediaFileRow'

export const AddMediaModal = () => {
	const [fileList, setFileList] = useState<FileList>()
	const fileInputRef = useRef<HTMLInputElement>()

	const handleFiles = useCallback(() => {
		const files = fileInputRef.current.files
		setFileList(files)
	}, [setFileList])

	return (
		<div>
			<div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
				<div>
					<h2>Add Media</h2>
				</div>
				<div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', paddingRight: 16}}>
					<label htmlFor='submit-file'>Upload</label>
				</div>
			</div>
			<form method='post' encType='multipart/form-data' action={urlFromEndpoint('upload-media')}>
				<input type='file' name='file[]' id='files' multiple directory='' webkitdirectory='' mozdirectory='' onChange={handleFiles} ref={fileInputRef} />
				<input type='submit' id='submit-file' className='hidden' disabled={!fileList} />
			</form>
			{!!fileList ? Array.from(fileList).map((file, idx) => <AddMediaFileRow file={file} key={String(idx)} />) : (
				<div>
					<p>No media selected</p>
				</div>
			)}
		</div>
	)
}