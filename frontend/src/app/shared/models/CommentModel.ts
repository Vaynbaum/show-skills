import { ShortUserResponseModel } from './ShortUserResponseModel';

export class CommentModel {
  constructor(
    public text: string,
    public name: string,
    public author: ShortUserResponseModel,
    public key: string,
    public date_create: number
  ) {}
}
