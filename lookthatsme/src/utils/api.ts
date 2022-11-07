export const API_ROOT = "http://lookthats.me/";

export enum ImageType {
    Montage = "montage",
    Similar = "similar"
}


export function getImage(type : ImageType) {
    return API_ROOT + type + "?t=" + String(Math.random());
}