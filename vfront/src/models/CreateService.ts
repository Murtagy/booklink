export class CreateService {
    constructor(
        public name: string,
        public seconds: number,
        public price?: number,
        public price_lower_bound?: number,
        public price_higher_bound?: number,
        public description?: string, 
    ){}
}