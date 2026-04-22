import api from '@/services/api';
import { headers } from '@/services/headers';

const takerService = {
  async fetchTakers(filter) {
    try {
      const params = { params: filter };
      const config = { ...headers(), ...params };
      const response = await api.get('takers/', config);
      return response;
    } catch (error) {
      console.error('Error fetching takers:', error);
      throw error;
    }
  },

  async postTaker(newTaker) {
    try {
      return await api.post('takers/', newTaker, headers());
    } catch (error) {
      console.error('Error creating taker:', error);
      throw error;
    }
  },

  async updateTaker(taker) {
    try {
      return await api.patch(`takers/${taker.id}/`, taker, headers());
    } catch (error) {
      console.error('Error updating taker:', error);
      throw error;
    }
  },

  async removeTaker(takerId) {
    try {
      return await api.delete(`takers/${takerId}`, headers());
    } catch (error) {
      console.error('Error removing taker:', error);
      throw error;
    }
  },

  async addDonate(donate) {
    try {
      return await api.post('donates/', donate, headers());
    } catch (error) {
      console.error('Error adding donate:', error);
      throw error;
    }
  },

  async updateDonate(donate) {
    try {
      return await api.patch(`donates/${donate.id}/`, donate, headers());
    } catch (error) {
      console.error('Error updating donate:', error);
      throw error;
    }
  },

  async stopDonate(takerId) {
    try {
      return await api.patch(`takers/${takerId}/stop_donate/`, null, headers());
    } catch (error) {
      console.error('Error stopping donate:', error);
      throw error;
    }
  },

  async removeDonate(donateId) {
    try {
      return await api.delete(`donates/${donateId}`, headers());
    } catch (error) {
      console.error('Error removing donate:', error);
      throw error;
    }
  }
};

export default takerService;
