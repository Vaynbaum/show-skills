import { SkillModel } from "./SkillModel";

export class UnloadPostModel {
  constructor(
    public name: string,
    public url_content: string,
    public skill:SkillModel
  ) {}
}
