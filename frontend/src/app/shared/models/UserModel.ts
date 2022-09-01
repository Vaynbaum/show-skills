import { LinkModel } from "./LinkModel";
import { RoleModel } from "./RoleModel";
import { ShortUserResponseModel } from "./ShortUserResponseModel";
import { SkillModel } from "./SkillModel";
import { SubscribeModel } from "./SubscribeModel";

export class UserModel {
  constructor(
    public username: string,
    public firstname: string,
    public lastname: string,
    public key: string,
    public url: string,
    public place_residence: string,
    public email: string,
    public birth_date: number,
    public folovers: ShortUserResponseModel[],
    public links: LinkModel[],
    public role: RoleModel,
    public skills: SkillModel,
    public subscriptions: SubscribeModel[],
    public role_key: string
  ) {}
}
