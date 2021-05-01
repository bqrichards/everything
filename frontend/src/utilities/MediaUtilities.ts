import moment from 'moment'
import { Media } from '../models/Media'

export const mediaIsEqual = (a: Media, b: Media) => {
	if (!a || !b) return a === b
	return a.id === b.id && a.date === b.date
}

export const initMedia = (media: Media) => {
	const newMedia = {...media}
	if (media.date) {
		newMedia.date = moment.utc(media.date).format('yyyy-MM-DDTHH:mm:ss.SSS')
	}

	return newMedia
}
