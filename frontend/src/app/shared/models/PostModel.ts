import { CommentModel } from './CommentModel';
import { LikeModel } from './LikeModel';
import { ShortUserResponseModel } from './ShortUserResponseModel';
import { SkillModel } from './SkillModel';

export class PostModel {
  constructor(
    public name: string,
    public url_content: string,
    public skill: SkillModel,
    public date_create: number,
    public author: ShortUserResponseModel,
    public likes: LikeModel[],
    public comments: CommentModel[],
    public key: string
  ) {}
}
