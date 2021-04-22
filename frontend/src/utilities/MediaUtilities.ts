import { Media } from '../models/Media'

export const mediaIsEqual = (a: Media, b: Media) => {
	if (!a || !b) return a === b
	return a.id === b.id && a.title === b.title && a.comment === b.comment && a.date === b.date
}
