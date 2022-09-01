import { ShortUserResponseModel } from "./ShortUserResponseModel";

export const Offline = 'Очно';
export const Online = 'Онлайн';
export class EventModel {
  constructor(
    public name: string,
    public date: number,
    public format_event: string,
    public place: object,
    public key:string,
    public author:ShortUserResponseModel
  ) {}
}
