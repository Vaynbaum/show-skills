import { ShortUserResponseModel } from './ShortUserResponseModel';

export class SubscribeModel {
  constructor(
    public favorite: ShortUserResponseModel,
    public number_visits: number
  ) {}
}
